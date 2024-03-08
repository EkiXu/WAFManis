FROM golang:1.18 AS builder

WORKDIR /build

ENV GOPROXY https://goproxy.cn
COPY go.mod .
COPY go.sum .
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOARCH=amd64 GOOS=linux go build -a -o main .

FROM alpine:3.10 AS final

WORKDIR /app
COPY --from=builder /build/main /app/
RUN adduser -D -u 10001 app-runner

USER app-runner
EXPOSE 6000
ENTRYPOINT ["/app/main"]
