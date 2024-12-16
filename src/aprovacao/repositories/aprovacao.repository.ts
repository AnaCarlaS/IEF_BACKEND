import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { gerenciamento_aprovacao } from '../entities/aprovacao.entities';


@Injectable()
export class Gerenciamento {
  constructor(
    @InjectRepository(gerenciamento_aprovacao)
    private readonly userRepository: Repository<gerenciamento_aprovacao>,
  ) {}

  findAll(): Promise<gerenciamento_aprovacao[]> {
    return this.userRepository.find();
  }

  
  findOne(id: number): Promise<gerenciamento_aprovacao> {
    return this.userRepository.findOne({ where: { id } });
  }

  create(user: gerenciamento_aprovacao): Promise<gerenciamento_aprovacao> {
    return this.userRepository.save(user);
  }

  async remove(id: number): Promise<void> {
    await this.userRepository.delete(id);
  }
}
