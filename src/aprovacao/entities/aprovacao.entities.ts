import { Entity, Column, PrimaryGeneratedColumn } from 'typeorm';

@Entity()
export class gerenciamento_aprovacao {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ type: 'float', nullable: true })
  status: number;

  @Column({ type: 'text', nullable: true })
  tipo: string;

  @Column({ type: 'text', nullable: true })
  codigo_solicitacao: string;

  @Column({ type: 'float', nullable: true})
  area: number;

  @Column({ type: 'float', nullable: true })
  modulos_fiscais: number;

  @Column({ type: 'text', nullable: true })
  municipio: string;

  @Column({ type: 'text', nullable: true })
  regional: string;

  @Column({ type: 'varchar', length: 255, nullable: true })
  pdf?: string;  

  @Column({ type: 'varchar', length: 255, nullable: true })
  localizacao?: string; 

  @Column({ type: 'timestamp', nullable: true })
  criacao: Date;

  @Column({ type: 'timestamp', nullable: true })
  atualizacao: Date;
}
