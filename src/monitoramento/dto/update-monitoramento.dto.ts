import {IsNumber, IsNotEmpty, IsString, IsOptional, IsUrl, IsDate} from 'class-validator';

export class UpdateGerenciamentoDto{

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

    @IsDate()
    @IsOptional()
    atualizacao: Date;

}