import { Injectable } from "@nestjs/common";
import { InjectRepository } from "@nestjs/typeorm";
import { gerenciamento_priorizacao } from "../entities/priorizacao.entities";
import { Repository } from "typeorm";


@Injectable()

export class Gerenciamento {

    constructor(
        @InjectRepository(gerenciamento_priorizacao)
        private readonly userRepository: Repository<gerenciamento_priorizacao>
    ){}

    findAll(): Promise <gerenciamento_priorizacao[]>{
        return this.userRepository.find();
    }

    findOne(id: number): Promise<gerenciamento_priorizacao>{
        return this.userRepository.findOne({ where: { id }});
    }

    create (user: gerenciamento_priorizacao): Promise <gerenciamento_priorizacao>{
        return this.userRepository.save(user);
    }

    async remove (id:number): Promise<void>{
        await this.userRepository.delete(id)
    }
}