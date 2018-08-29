import com.pilosa.client.CountResultItem;
import com.pilosa.client.PilosaClient;
import com.pilosa.client.QueryResponse;
import com.pilosa.client.exceptions.PilosaException;
import com.pilosa.client.orm.*;

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

        String datasetPath = args[0];
        String address = (args.length > 1)? args[1] : ":10101";
        PilosaClient client = PilosaClient.withAddress(address);
        List<String> languageNames = loadLanguageNames(datasetPath);
        runQueries(client, languageNames);
    }

    private static List<String> loadLanguageNames(String datasetPath) throws IOException {
        List<String> result = new ArrayList<>();
        try (Stream<String> stream = Files.lines(Paths.get(datasetPath, "languages.txt"))) {
            stream.forEach(result::add);
        }
        return result;
    }

    private static void runQueries(PilosaClient client, List<String> languageNames) {
        // Let's load the schema from the server.
        Schema schema;
        try {
            schema = client.readSchema();
        }
        catch (PilosaException ex) {
            // Most calls will return an error value.
            // You should handle them appropriately.
            // We will just terminate the program in this case.
            throw new RuntimeException(ex);
        }

        // We need to refer to indexes and fields before we can use them in a query.
        Index repository = schema.index("repository");
        Field stargazer = repository.field("stargazer");
        Field language = repository.field("language");

        QueryResponse response;
        PqlQuery query;
        List<Long> repositoryIDs;

        // Which repositories did user 14 star:
        response = client.query(stargazer.row(14));
        repositoryIDs = response.getResult().getRow().getColumns();
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
                stargazer.row(14),
                stargazer.row(19)
        );
        response = client.query(query);
        repositoryIDs = response.getResult().getRow().getColumns();
        System.out.println("Both user 14 and 19 starred:");
        printIDs(repositoryIDs);

        System.out.println();

        // Which repositories were starred by user 14 or 19:
        query = repository.union(
                stargazer.row(14),
                stargazer.row(19)
        );
        response = client.query(query);
        repositoryIDs = response.getResult().getRow().getColumns();
        System.out.println("User 14 or 19 starred:");
        printIDs(repositoryIDs);

        System.out.println();

        // Which repositories were starred by user 14 or 19 and were written in language 1:
        query = repository.intersect(
                repository.union(
                        stargazer.row(14),
                        stargazer.row(19)
                ),
                language.row(1)
        );
        response = client.query(query);
        repositoryIDs = response.getResult().getRow().getColumns();
        System.out.println("User 14 or 19 starred, written in language 1:");
        printIDs(repositoryIDs);

        System.out.println();

        // Set user 99999 as a stargazer for repository 77777:
        client.query(stargazer.set(99999, 77777));
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
            System.out.printf("\t%d. %s (%d stars)\n", ++i, languageNames.get((int) item.getID()), item.getCount());
        }
    }
}