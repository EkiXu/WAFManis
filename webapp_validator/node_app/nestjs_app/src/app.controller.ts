import { Body, Controller, Get, Header, Post,UploadedFile,UseInterceptors } from '@nestjs/common';
import { FileInterceptor } from '@nestjs/platform-express';
import { AppService } from './app.service';

@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  // @Get()
  // getHello(): string {
  //   return this.appService.getHello();
  // }

  @Post('')
  @Header('Content-Type', 'application/json')
  @UseInterceptors(FileInterceptor('file'))
  echo(@Body() body) {
    // console.log(file);
    // console.log(body);
    return JSON.stringify({form:body})
  }
}
