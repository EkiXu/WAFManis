class EchoController < ApplicationController
  skip_forgery_protection
  def get
    res = Hash["query" => params]
    render json: res
  end
  def post
    res = Hash["form" => params]
    render json: res
  end
end
