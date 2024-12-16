import { Injectable, NotFoundException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { gerenciamento_aprovacao } from './entities/aprovacao.entities';
import { CreateGerenciamentoDto } from './dto/create-aprovacao.dto';
import { UpdateGerenciamentoDto } from './dto/update-aprovacao.dto';

@Injectable()
export class GerenciamentoService {
  constructor(
    @InjectRepository(gerenciamento_aprovacao)
    private readonly gerenciamentoRepository: Repository<gerenciamento_aprovacao>,
  ) {}

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

  async create(createGerenciamentoDto: CreateGerenciamentoDto): Promise<gerenciamento_aprovacao> {
    try {
      const newRecord = this.gerenciamentoRepository.create({
        ...createGerenciamentoDto, // Inclui os dados enviados pelo cliente
        criacao: new Date(), // Adiciona a data atual ao campo 'criacao'
      });
  
      return await this.gerenciamentoRepository.save(newRecord);
    } catch (error) {
      console.error('Error saving Gerenciamento:', error);
      throw error; // Propaga o erro para que o NestJS trate
    }
  }
  
/*
  async findAll(): Promise<gerenciamento_aprovacao[]> {
    return this.gerenciamentoRepository.find();
  }
    */

  async update(
    id: number,
    updateGerenciamentoDto: UpdateGerenciamentoDto,
  ): Promise<gerenciamento_aprovacao> {
    const existingRecord = await this.gerenciamentoRepository.findOneBy({ id });

    if (!existingRecord) {
      throw new NotFoundException(`Record with ID ${id} not found`);
    }

    Object.assign(existingRecord, updateGerenciamentoDto, {atualizacao: new Date ()}); // Atualiza os campos enviados
    return this.gerenciamentoRepository.save(existingRecord); // Salva no banco
  }

  async remove(id: number): Promise<string> {
    const result = await this.gerenciamentoRepository.delete(id); // Remove o registro

    if (result.affected === 0) {
      // Se nenhum registro foi afetado, o ID não existe
      throw new NotFoundException(`ID ${id} não encontrado`);
    }

    return `ID ${id} excluído com sucesso`;
  }
}
