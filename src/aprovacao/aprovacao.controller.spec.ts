import { Test, TestingModule } from '@nestjs/testing';
import { GerenciamentoController } from './aprovacao.controller';
import { GerenciamentoService } from './aprovacao.service';

const mockService = () => ({
  findAll: jest.fn(),
  create: jest.fn(),
  update: jest.fn(),
  remove: jest.fn(),
});

describe('GerenciamentoController', () => {
  let controller: GerenciamentoController;
  let service: jest.Mocked<GerenciamentoService>;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [GerenciamentoController],
      providers: [
        { provide: GerenciamentoService, useValue: mockService() },
      ],
    }).compile();

    controller = module.get<GerenciamentoController>(GerenciamentoController);
    service = module.get<GerenciamentoService>(GerenciamentoService) as jest.Mocked<GerenciamentoService>;
  });

  it('Serviço instanciado com sucesso!', () => {
    expect(controller).toBeDefined();
  });

  describe('findAll', () => {
    it('Registros retornados com sucesso!', async () => {
      const mockResult = { data: [], total: 0 };
      service.findAll.mockResolvedValue(mockResult);

      const result = await controller.findAll(1, 7);

      expect(service.findAll).toHaveBeenCalledWith(1, 7);
      expect(result).toEqual(mockResult);
    });
  });

  describe('create', () => {
    it('Criação de registros feito com sucesso!', async () => {
      const mockDto = { status: 1, tipo: 'Novo' } as any;
      const mockEntity = { id: 1, ...mockDto };
      service.create.mockResolvedValue(mockEntity);

      const result = await controller.create(mockDto);

      expect(service.create).toHaveBeenCalledWith(mockDto);
      expect(result).toEqual(mockEntity);
    });
  });

  describe('update', () => {
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


      const result = await controller.update(1, mockDto);

      expect(service.update).toHaveBeenCalledWith(1, mockDto);
      expect(result).toEqual(mockEntity);
    });
  });

  describe('remove', () => {
    it('Registro removido com sucesso!', async () => {
      const mockMessage = 'ID 1 excluído com sucesso';
      service.remove.mockResolvedValue(mockMessage);

      const result = await controller.remove(1);

      expect(service.remove).toHaveBeenCalledWith(1);
      expect(result).toEqual(mockMessage);
    });
  });
});
