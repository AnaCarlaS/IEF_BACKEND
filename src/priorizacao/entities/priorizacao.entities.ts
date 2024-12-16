import { Column, Entity, PrimaryGeneratedColumn } from "typeorm";

@Entity()
export class gerenciamento_priorizacao{
    @PrimaryGeneratedColumn()
    id: number;

    @Column()
    status: number;

    @Column() 
    tipo: string;

    @Column() 
    codigo_solicitacao: string;

    @Column()
    area: number;

    @Column()
    municipio: string;

    @Column()
    regional: string; 

    @Column()
    ordem: number;

    @Column()
    prioridade: string;

    @Column()
    nota: number;

    @Column({ type: 'text', nullable: true })
    pdf: string;

    @Column({ type: 'timestamp', nullable: true })
    criacao: Date;
  
    @Column({ type: 'timestamp', nullable: true })
    atualizacao: Date;

}
