import { Module } from "@nestjs/common";
import { TypeOrmModule } from "@nestjs/typeorm";
import { GerenciamentoController } from "./monitoramento.controller";
import { gerenciamento_monitoramento } from "./entities/monitoramento.entities";
import { GerenciamentoService } from "./monitoramento.service";

@Module({
    imports: [TypeOrmModule.forFeature([gerenciamento_monitoramento])],
    controllers: [GerenciamentoController],
    providers: [GerenciamentoService],
})
export class MonitoramentoModule {}
