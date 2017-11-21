import com.pilosa.client.CountResultItem;
import com.pilosa.client.PilosaClient;
import com.pilosa.client.QueryResponse;
import com.pilosa.client.TimeQuantum;
import com.pilosa.client.orm.*;
//import org.apache.logging.log4j.Level;
//import org.apache.logging.log4j.status.StatusLogger;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Stream;

public class StarTrace {
    public static void main(String []args) throws IOException {
        if (args.length < 1) {
            System.err.printf("Usage: java -jar startrace.jar PATH_TO_DATASET [PILOSA_ADDRESS]\n\n");
            System.exit(1);
        }

        // Turn off no logger configured notification
//        StatusLogger.getLogger().setLevel(Level.OFF);

        String datasetPath = args[0];
        String address = (args.length > 1)? args[1] : ":10101";
        PilosaClient client = PilosaClient.withAddress(address);
        List<String> languageNames = loadLanguageNames(datasetPath);
        runQueries(client, languageNames);
    }

    private static List<String> loadLanguageNames(String datasetPath) throws IOException {
        List<String> result = new ArrayList<>();
        try(Stream<String> stream = Files.lines(Paths.get(datasetPath, "languages.txt"))) {
            stream.forEach(result::add);
        }
        return result;
    }

    private static void runQueries(PilosaClient client, List<String> languageNames) {
        Schema schema = new Schema();
        Index repository = schema.getRepository();
        Frame stargazer = schema.getStargazer();
        Frame language = schema.getLanguage();

        QueryResponse response;
        PqlQuery query;
        List<Long> repositoryIDs;

        // Which repositories did user 14 star:
        response = client.query(stargazer.bitmap(14));
        repositoryIDs = response.getResult().getBitmap().getBits();
        System.out.println("User 14 starred:");
        printIDs(repositoryIDs);

        System.out.println();

        // What are the top 5 languages in the sample data:
        response = client.query(language.topN(5));
        List<CountResultItem> top_languages = response.getResult().getCountItems();
        System.out.println("Top Languages:");
        printTopNLanguages(top_languages, languageNames);

        System.out.println();

        // Which repositories were starred by both user 14 and 19:
        query = repository.intersect(
                stargazer.bitmap(14),
                stargazer.bitmap(19)
        );
        response = client.query(query);
        repositoryIDs = response.getResult().getBitmap().getBits();
        System.out.println("User 14 and 19 starred:");
        printIDs(repositoryIDs);

        System.out.println();

        // Which repositories were starred by either user 14 or 19:
        query = repository.union(
                stargazer.bitmap(14),
                stargazer.bitmap(19)
        );
        response = client.query(query);
        repositoryIDs = response.getResult().getBitmap().getBits();
        System.out.println("User 14 or 19 starred:");
        printIDs(repositoryIDs);

        System.out.println();

        // Which repositories were starred by user 14 and 19 and also were written in language 1:
        query = repository.intersect(
                repository.intersect(
                        stargazer.bitmap(14),
                        stargazer.bitmap(19)
                ),
                language.bitmap(1)
        );
        response = client.query(query);
        repositoryIDs = response.getResult().getBitmap().getBits();
        System.out.println("User 14 and 19 starred and in language 1:");
        printIDs(repositoryIDs);

        System.out.println();

        // Set user 99999 as a stargazer for repository 77777:
        client.query(stargazer.setBit(99999, 77777));
        System.out.printf("Set user 99999 as a stargazer for repository 77777\n\n");
    }

    private static void printIDs(List<Long> ids) {
        int i = 0;
        for (Long id : ids) {
            System.out.printf("\t%d. %d\n", ++i, id);
        }
    }

    private static void printTopNLanguages(List<CountResultItem> items, List<String> languageNames) {
        int i = 0;
        for (CountResultItem item : items) {
            System.out.printf("\t%d. %s (%d stars)\n", ++i, languageNames.get((int)item.getID()), item.getCount());
        }
    }

    static final class Schema {
        Schema() {
            this.repository = Index.withName("repository");

            FrameOptions stargazerFrameOptions = FrameOptions.builder()
                    .setTimeQuantum(TimeQuantum.YEAR_MONTH_DAY)
                    .setInverseEnabled(true)
                    .build();
            this.stargazer = this.repository.frame("stargazer", stargazerFrameOptions);

            FrameOptions languageFrameOptions = FrameOptions.builder()
                    .setInverseEnabled(true)
                    .build();
            this.language = this.repository.frame("language", languageFrameOptions);
        }

        Index getRepository() {
            return this.repository;
        }

        Frame getStargazer() {
            return this.stargazer;
        }

        Frame getLanguage() {
            return this.language;
        }

        private Index repository;
        private Frame stargazer;
        private Frame language;
    }
}
