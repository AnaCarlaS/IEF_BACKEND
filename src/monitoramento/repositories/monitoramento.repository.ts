import { Injectable } from "@nestjs/common";
import { InjectRepository } from "@nestjs/typeorm";
import { gerenciamento_monitoramento } from "../entities/monitoramento.entities";
import { Repository } from "typeorm";

@Injectable()

export class Gerenciamento {

    constructor(
        @InjectRepository(gerenciamento_monitoramento)
        private readonly userRepository: Repository<gerenciamento_monitoramento>
    ){}

    findAll(): Promise <gerenciamento_monitoramento[]>{
        return this.userRepository.find();
    }

    findOne(id: number): Promise<gerenciamento_monitoramento>{
        return this.userRepository.findOne({ where: { id }});
    }

    create (user: gerenciamento_monitoramento): Promise <gerenciamento_monitoramento>{
        return this.userRepository.save(user);
    }

    async remove (id:number): Promise<void>{
        await this.userRepository.delete(id)
    }
}