import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { GerenciamentoController } from './priorizacao.controller';
import { gerenciamento_priorizacao } from './entities/priorizacao.entities';
import { GerenciamentoService } from './priorizacao.service';

@Module({
    imports: [TypeOrmModule.forFeature([gerenciamento_priorizacao])],
    controllers: [GerenciamentoController],
    providers: [GerenciamentoService],
})
export class PriorizacaoModule {}
