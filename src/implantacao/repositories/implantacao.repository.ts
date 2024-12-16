import { Injectable } from "@nestjs/common";
import { InjectRepository } from "@nestjs/typeorm";
import { gerenciamento_implantacao } from "../entities/implantacao.entities";
import { Repository } from "typeorm";


@Injectable()

export class Gerenciamento {

    constructor(
        @InjectRepository(gerenciamento_implantacao)
        private readonly userRepository: Repository<gerenciamento_implantacao>
    ){}

    findAll(): Promise <gerenciamento_implantacao[]>{
        return this.userRepository.find();
    }

    findOne(id: number): Promise<gerenciamento_implantacao>{
        return this.userRepository.findOne({ where: { id }});
    }

    create (user: gerenciamento_implantacao): Promise <gerenciamento_implantacao>{
        return this.userRepository.save(user);
    }

    async remove (id:number): Promise<void>{
        await this.userRepository.delete(id)
    }
}