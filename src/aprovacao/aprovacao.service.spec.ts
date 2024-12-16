import { Repository } from "typeorm"
import { GerenciamentoService } from "./aprovacao.service";
import { gerenciamento_aprovacao } from "./entities/aprovacao.entities";
import { TestingModule, Test } from "@nestjs/testing";
import { getRepositoryToken } from "@nestjs/typeorm";
import { Controller } from "@nestjs/common";



const mockRpository = () =>({

    //criando um mock - jest.fn criar uma função simulada para retornar valores e verificaçoes
    findAndCount: jest.fn(), //encotrar e contar quantos registros foram encotrados
    save: jest.fn(), // salva no banco de dados 
    findOneBy: jest.fn(), // busca um registro aprtir de um filtro
    delete: jest.fn(), // exclui a entidade do banco 
});

//mockrepository é um tipo que definie o mock 
// keyof repsoturo<T> recbem todas os metodos disposniveis (find,save,delete...)
//record cria um objetos onde cada metodos od repsositorio sera uma função mokca
type mockRpository<T =any> = Partial <Record<keyof Repository<T>, jest.Mock>>;

//descrevebdo um oc==conjunto de teste relacioandos ao gerenicamento service
describe('GerenciamentoService',() => {
    let service: GerenciamentoService;
    let repository: mockRpository<gerenciamento_aprovacao>; //um mock do typeorm  sendo injetado no serviço

    beforeEach(async() => {
        const module: TestingModule = await Test.createTestingModule({
            providers:[
                GerenciamentoService, // registra o serviço que estamos usando
                {
                    provide: getRepositoryToken(gerenciamento_aprovacao), // regista ao mock
                    useValue: mockRpository(), // usa o mock deifinido anteiror mente
                },
            ],
        
    }).compile(); //compilando o modulo 

    service = module.get<GerenciamentoService>(GerenciamentoService);
    repository = module.get<mockRpository<gerenciamento_aprovacao>>(
        getRepositoryToken(gerenciamento_aprovacao),
    );
});    

    // teste para ver se o serviços foi isntanciado
    it('Serviço instanciado com sucesso!', () =>{
        expect(service).toBeDefined(); // garante que a instancia do serviço nao seja sem definição
    });

    describe('findAll', () => {
        it('Registros retornados com sucesso!',async ()=> {
            const mockData = [{id:1 , tipo: 'Fomento'}];
            repository.findAndCount.mockResolvedValue([mockData, 1]); // codfirar o mock para simular o retonro esprado  do fundandcount
        
            const result = await service.findAll(1,7);

            expect(repository.findAndCount).toHaveBeenCalledWith({ //verifica o mentdo findandcount foi chaamdo com os argumento corretos
                skip:0,
                take: 7,
            });
            expect(result).toEqual({data: mockData, total: 1}); // ga q o retorno do serviço esta correto

        });
    });    
    
    describe('create', () =>{
        it('Criação de registros feito com sucesso!',async() => {
            const mockDto = { status: 1, tipo:'Mudas'} as any;
            const mockEntity = {id: 1, ...mockDto};
            jest.spyOn(service, 'create').mockResolvedValue(mockEntity);

            const result = await service.create( mockDto);

            expect(service.create).toHaveBeenCalledWith(mockDto);
            expect(result).toEqual(mockEntity);
        });
    });
    
    describe('update', () =>{
        it('Update feito com sucesso!', async () => {
            const mockDto = {tipo:'Mudas'};
            //teste 
            const mockEntity = {
                id: 1,
                tipo: 'Fomento',
                codigo_solicitacao: 'REQ-2024123',
                area: 20.3,
                modulos_fiscais: 23,
                municipio: 'Florestal',
                regional: 'Central',
                pdf: 'termo1.pdf',
                localizacao: 'localizacao',
                status: 1, 
                criacao: new Date('2024-01-01'), 
                atualizacao: new Date('2024-01-02'), 
            };
    
            jest.spyOn(service, 'update').mockResolvedValue(mockEntity);

            const result = await service.update(1, mockDto);
            
          
            expect(result).toEqual(mockEntity);
        });
    });    

    describe('remove',() => {
        it('Registro removido com sucesso!',async () =>{
            const mockMessage = 'ID 1 excluido com suceeso' ;
            jest.spyOn(service, 'remove').mockResolvedValue(mockMessage);
            const result = await service.remove(1);

            expect(service.remove).toHaveBeenCalledWith(1);
            expect(result).toEqual(mockMessage);
        });
    });
});
    