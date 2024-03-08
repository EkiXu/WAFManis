FROM mcr.microsoft.com/dotnet/aspnet:6.0

WORKDIR /app 
EXPOSE 80

RUN apt update &&apt install -y wget

COPY . .


#ENTRYPOINT ["dotnet", "watch","run"]
CMD [ "dotnet","./bin/Debug/net6.0/fuzz_aspnet_core.dll" ]