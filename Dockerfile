FROM pilosa/pilosa:v1.2.0 AS pilosa
FROM ubuntu:18.04 AS build

COPY ./language.csv /getting-started/language.csv
COPY ./stargazer.csv /getting-started/stargazer.csv
COPY ./docker/create-schema.sh /getting-started/create-schema.sh
COPY --from=pilosa /pilosa /pilosa

RUN sh /getting-started/create-schema.sh

FROM scratch

COPY --from=build /pilosa /pilosa
COPY --from=build /data /data

ENTRYPOINT ["/pilosa"]
CMD ["server", "--data-dir", "/data", "--bind", "http://0.0.0.0:10101"]
