/* Status: numero inteiro, tipo: string, código de solicitação: string , 
área: numero racional , módulos fiscais: numero racional, módulos fiscais: numero racional, 
progresso:  numero inteiro, município: string, regional: string, anexo: string
*/

// Tem que ver se o anexo é opcional

import {IsNumber, IsNotEmpty, IsString, IsOptional, IsUrl, IsDate} from 'class-validator';

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

    @IsNumber()
    @IsNotEmpty()
    modulo_fiscal: number;

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
    anexo: string;

    @IsDate()
    @IsOptional()
    criacao: Date;

}