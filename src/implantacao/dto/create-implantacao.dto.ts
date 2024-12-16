import {IsNumber, IsNotEmpty, IsString,IsDate,IsOptional,IsUrl } from 'class-validator';

export class CreateGerenciamentoDto{

    @IsNumber()
    @IsNotEmpty()
    status:number;

    @IsString()
    @IsNotEmpty()
    tipo:string;

    @IsString()
    @IsNotEmpty()
    codigo_solicitacao:string;

    @IsNumber()
    @IsNotEmpty()
    area: number;

    @IsNumber()
    @IsNotEmpty()
    modulos_fiscais: number;

    @IsString()
    @IsNotEmpty()
    ano: string;

    @IsNumber()
    @IsNotEmpty()
    progresso: number;

    @IsString()
    @IsNotEmpty()
    municipio: string;

    @IsString()
    @IsNotEmpty()
    regional: string;

    @IsString()
    @IsOptional()
    @IsUrl()
    pdf: string;

    @IsDate()
    @IsOptional()
    criacao: Date;

}