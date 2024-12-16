import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { GerenciamentoController } from './aprovacao.controller';
import { GerenciamentoService } from './aprovacao.service';
import { gerenciamento_aprovacao } from './entities/aprovacao.entities';
@Module({

    imports: [TypeOrmModule.forFeature([gerenciamento_aprovacao])],
    controllers: [GerenciamentoController],
    providers: [GerenciamentoService],
})
export class AprovacaoModule {}
