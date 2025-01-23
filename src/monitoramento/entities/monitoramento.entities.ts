import { Column, Entity, PrimaryGeneratedColumn } from "typeorm";

@Entity()
export class gerenciamento_monitoramento{
    @PrimaryGeneratedColumn()
    id: number;

    @Column()
    status: number;

    @Column() 
    tipo: string;

    @Column() 
    codigo_solicitacao: string;

    @Column({type: 'float', nullable: true})
    area: number;

    @Column()
    modulo_fiscal: number;

    @Column()
    progresso: number;

    @Column()
    municipio: string;

    @Column()
    regional: string; 

    @Column({ type: 'text', nullable: true })
    anexo: string;

    @Column({ type: 'timestamp', nullable: true })
    criacao: Date;
  
    @Column({ type: 'timestamp', nullable: true })
    atualizacao: Date;

}