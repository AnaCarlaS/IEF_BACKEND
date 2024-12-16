import { Column, Entity, PrimaryGeneratedColumn } from "typeorm";


@Entity()
export class gerenciamento_implantacao{
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
    modulos_fiscais: number;

    @Column()
    ano: string;

    @Column()
    progresso: number;

    @Column()
    municipio: string;

    @Column()
    regional: string;

    @Column({ type: 'text', nullable: true })
    pdf: string;

    @Column({ type: 'timestamp', nullable: true })
    criacao: Date;
  
    @Column({ type: 'timestamp', nullable: true })
    atualizacao: Date;

}
