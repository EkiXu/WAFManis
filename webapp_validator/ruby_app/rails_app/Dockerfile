FROM ruby:2.7.0

WORKDIR /app
COPY Gemfile* .

RUN bundle install

COPY . .

EXPOSE 3000

CMD ["rails", "server", "-b", "0.0.0.0"]