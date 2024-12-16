import { IsNumber, IsOptional, IsString, IsDate,IsUrl } from "class-validator";

export class UpdateGerenciamentoDto{

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

    @IsString()
    @IsOptional()
    municipio?: string;

    @IsString()
    @IsOptional()
    regional?: string;

    @IsNumber()
    @IsOptional()
    ordem?: number;

    @IsString()
    @IsOptional()
    prioridade?: string;

    @IsString()
    @IsOptional()
    nota?: number;

    @IsString()
    @IsOptional()
    @IsUrl()
    pdf?: string;

    @IsDate()
    @IsOptional()
    atualizacao?: Date;

}