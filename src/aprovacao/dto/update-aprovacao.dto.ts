import { IsString, IsNumber, IsOptional, IsDate, IsNotEmpty, IsUrl } from 'class-validator';

export class UpdateGerenciamentoDto {
  @IsNumber()
  @IsOptional()
  status?: number;

  @IsString()
  @IsOptional()
  tipo?: string;

  @IsString()
  @IsOptional()
  codigo_solicitacao?: string;

  @IsNumber()
  @IsOptional()
  area?: number;

  @IsNumber()
  @IsOptional()
  modulos_fiscais?: number;

  @IsString()
  @IsOptional()
  municipio?: string;

  @IsString()
  @IsOptional()
  regional?: string;

  @IsUrl()
  @IsOptional()
  pdf?: string;

  @IsUrl()
  @IsOptional()
  localizacao?: string;

  @IsDate()
  @IsOptional()
  atualizacao?: Date;

  
}
