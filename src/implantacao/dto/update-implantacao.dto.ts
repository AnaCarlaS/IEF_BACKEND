import { IsNumber, IsOptional, IsString, IsDate,IsUrl } from "class-validator";

export class UpdateGerenciamentoDto{

    @IsNumber()
    @IsOptional()
    status?: number;

    @IsString()
    @IsOptional()
    tipo: string;

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
    ano?: string;

    @IsNumber()
    @IsOptional()
    progresso?: number;

    @IsString()
    @IsOptional()
    municipio?: string;

    @IsString()
    @IsOptional()
    regional?: string;

    @IsString()
    @IsOptional()
    @IsUrl()
    pdf?: string;

    @IsDate()
    @IsOptional()
    atualizacao?: Date;

}