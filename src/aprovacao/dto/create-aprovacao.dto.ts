import { IsString, IsNumber, IsNotEmpty, IsDate, IsOptional,IsUrl } from 'class-validator';

export class CreateGerenciamentoDto {
  @IsNumber()
  @IsNotEmpty()
  status: number;

  @IsString()
  @IsNotEmpty()
  tipo: string;

  @IsString()
  @IsNotEmpty()
  codigo_solicitacao: string;

  @IsNumber()
  @IsNotEmpty()
  area: number;

  @IsNumber()
  @IsNotEmpty()
  modulos_fiscais: number;

  @IsString()
  @IsNotEmpty()
  municipio: string;

  @IsString()
  @IsNotEmpty()
  regional: string;

  @IsUrl()
  @IsOptional()
  pdf?: string;

  @IsUrl()
  @IsOptional()
  localizacao?: string;

  @IsDate()
  @IsOptional()
  criacao: Date;
}
