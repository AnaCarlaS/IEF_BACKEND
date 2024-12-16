import { Injectable, NotFoundException } from "@nestjs/common";
import { InjectRepository } from "@nestjs/typeorm";
import { gerenciamento_priorizacao } from "./entities/priorizacao.entities";
import { Repository } from "typeorm";
import { CreateGerenciamentoDto } from "./dto/create-priorizacao.dto";
import { UpdateGerenciamentoDto } from './dto/update-priorizacao.dto';

@Injectable()
export class GerenciamentoService{

   constructor(
    @InjectRepository(gerenciamento_priorizacao)
    private readonly gerenciamentoRepository: Repository<gerenciamento_priorizacao>,
   ){} 

   async create(createGerenciamentoDto: CreateGerenciamentoDto): Promise <gerenciamento_priorizacao>{
    try {
        const newRecord = this.gerenciamentoRepository.create({
            ...createGerenciamentoDto, 
            criacao: new Date(),
        } );

        return await this.gerenciamentoRepository.save(newRecord);
    }catch(error){
        console.log('Error: ', error);
        throw error;
    }
   }

   async findAll(page: number = 1, pageSize: number = 7) {
    const [data, total] = await this.gerenciamentoRepository.findAndCount({
      skip: (page - 1) * pageSize,
      take: pageSize,
    });
    return {
      data,
      total,
    };
  }


   /*async findAll(): Promise<gerenciamento_priorizacao[]> {
        return this.gerenciamentoRepository.find();
   }*/

   async update(id: number, updateGerenciamentoDto: UpdateGerenciamentoDto,): Promise <gerenciamento_priorizacao>{

    const existingRecord = await this.gerenciamentoRepository.findOneBy({ id });
    if (!existingRecord) {
        throw new NotFoundException(`Record with ID ${id} not found`);
      }

      Object.assign(existingRecord, updateGerenciamentoDto, {atualizacao: new Date ()}); 
      return this.gerenciamentoRepository.save(existingRecord); 
   }

   async remove(id: number): Promise<string>{
    const result =  await this.gerenciamentoRepository.delete(id);

    if (result.affected === 0) {
        // Se nenhum registro foi afetado, o ID não existe
        throw new NotFoundException(`ID ${id} não encontrado`);
      }
  
      return `ID ${id} excluído com sucesso`;
   }
   
}