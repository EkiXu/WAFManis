FROM rust:1.72.0 as builder
WORKDIR /usr/src/app

# accerlate with mirror in China
RUN touch $CARGO_HOME/config \
    && echo '[source.crates-io]' > $CARGO_HOME/config \
    && echo 'registry = "https://github.com/rust-lang/crates.io-index"'  >> $CARGO_HOME/config \
    && echo "replace-with = 'tuna'"  >> $CARGO_HOME/config \
    && echo '[source.tuna]'   >> $CARGO_HOME/config \
    && echo 'registry = "https://mirrors.tuna.tsinghua.edu.cn/git/crates.io-index.git"'  >> $CARGO_HOME/config \
    && echo '[net]'   >> $CARGO_HOME/config \
    && echo 'git-fetch-with-cli = true'   >> $CARGO_HOME/config \
    && echo '' >> $CARGO_HOME/config

COPY . .
RUN cargo build --release

CMD ["cargo","run","--release"]
