import {IsNumber, IsNotEmpty, IsString,IsDate,IsOptional,IsUrl } from 'class-validator';

export class CreateGerenciamentoDto{

    @IsNumber()
    @IsNotEmpty()
    status:number;

    @IsNumber()
    @IsNotEmpty()
    tipo:string;

    @IsString()
    @IsNotEmpty()
    codigo_solicitacao:string;

    @IsNumber()
    @IsNotEmpty()
    area: number;

    @IsString()
    @IsNotEmpty()
    municipio: string;

    @IsString()
    @IsNotEmpty()
    regional: string;

    @IsNumber()
    @IsNotEmpty()
    ordem: number;

    @IsString()
    @IsNotEmpty()
    prioridade: string;

    @IsString()
    @IsNotEmpty()
    nota: number;

    @IsString()
    @IsOptional()
    @IsUrl()
    pdf: string;

    @IsDate()
    @IsOptional()
    criacao: Date;

}