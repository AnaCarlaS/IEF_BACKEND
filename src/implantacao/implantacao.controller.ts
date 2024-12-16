import { Body, Controller, Delete, Get, Param, Patch, Post, Put, Query } from '@nestjs/common';
import { GerenciamentoService } from './implantacao.service';
import { CreateGerenciamentoDto } from './dto/create-implantacao.dto';
import { UpdateGerenciamentoDto } from './dto/update-implantacao.dto';

@Controller('implantacao')
export class GerenciamentoController {

    constructor(private readonly gerenciamentoservice: GerenciamentoService){}

    @Post()
    create(@Body() createGerenciamentoDto :CreateGerenciamentoDto){
        return this.gerenciamentoservice.create(createGerenciamentoDto)
    }

    /*
    @Get()
    findAll(){
        return this.gerenciamentoservice.findAll();
    }*/

    @Get()
    findAll(@Query('page') page = 1, @Query('pageSize') pageSize = 7) {
        return this.gerenciamentoservice.findAll(page, pageSize);
    }

    @Patch(':id')
    update(
      @Param('id') id: number, // Pega o ID da URL
      @Body() updateGerenciamentoDto: UpdateGerenciamentoDto, // Dados do corpo
    ) {
      return this.gerenciamentoservice.update(id, updateGerenciamentoDto);
    }
  

    @Delete(':id')
    remove(@Param('id') id: number){
        return this.gerenciamentoservice.remove(id);
    }

}