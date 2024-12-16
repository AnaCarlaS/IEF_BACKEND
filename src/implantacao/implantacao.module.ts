import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { GerenciamentoController } from './implantacao.controller';
import { gerenciamento_implantacao } from './entities/implantacao.entities';
import { GerenciamentoService } from './implantacao.service';

@Module({
    imports: [TypeOrmModule.forFeature([gerenciamento_implantacao])],
    controllers: [GerenciamentoController],
    providers: [GerenciamentoService],
})
export class ImplantacaoModule {}
