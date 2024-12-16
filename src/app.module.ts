import { Module } from '@nestjs/common'; 
import { AppController } from './app.controller'; 
import { AppService } from './app.service'; 
import { TypeOrmModule } from '@nestjs/typeorm'; 
import { gerenciamento_aprovacao } from './aprovacao/entities/aprovacao.entities';
import { AprovacaoModule } from './aprovacao/aprovacao.module';
import { gerenciamento_priorizacao } from './priorizacao/entities/priorizacao.entities';
import { PriorizacaoModule } from './priorizacao/priorizacao.module';
import { gerenciamento_implantacao } from './implantacao/entities/implantacao.entities';
import { ImplantacaoModule } from './implantacao/implantacao.module';
import { MonitoramentoModule } from './Monitoramento/monitoramento.module';
import { gerenciamento_monitoramento } from './Monitoramento/entities/monitoramento.entities';

@Module({
  imports: [
    TypeOrmModule.forRoot({
      type: 'postgres',
      host: 'localhost',       // Endereço do servidor do banco de dados
      port: 5432,              // Porta padrão do PostgreSQL
      username: 'postgres', // Nome do usuário do banco de dados
      password: '123',   // Senha do banco de dados
      database: 'postgres', // Nome do banco de dados
      entities: [gerenciamento_aprovacao, gerenciamento_priorizacao,gerenciamento_implantacao, gerenciamento_monitoramento], // Entidades
      synchronize: true,       // Sincroniza o esquema do banco de dados, apenas para desenvolvimento
      logging: true, //Ativa logs para visualizarmos possíveis erros
    }),
    AprovacaoModule,
    PriorizacaoModule,
    ImplantacaoModule,
    MonitoramentoModule,
  ],
  controllers: [AppController],
  providers: [AppService],
})

export class AppModule {}
