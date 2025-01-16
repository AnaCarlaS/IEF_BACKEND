import { Test, TestingModule } from '@nestjs/testing';
import { GerenciamentoService } from './monitoramento.service';
import { Repository } from 'typeorm';
import { getRepositoryToken } from '@nestjs/typeorm';
import { gerenciamento_monitoramento } from './entities/monitoramento.entities';
import { NotFoundException } from '@nestjs/common';
import { CreateGerenciamentoDto } from './dto/create-monitoramento.dto';
import { UpdateGerenciamentoDto } from './dto/update-monitoramento.dto';

describe('GerenciamentoService', () => {
  let service: GerenciamentoService;
  let repository: Repository<gerenciamento_monitoramento>;

  const mockRepository = {
    create: jest.fn(),
    save: jest.fn(),
    findAndCount: jest.fn(),
    findOneBy: jest.fn(),
    delete: jest.fn(),
  };

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        GerenciamentoService,
        {
          provide: getRepositoryToken(gerenciamento_monitoramento),
          useValue: mockRepository,
        },
      ],
    }).compile();

    service = module.get<GerenciamentoService>(GerenciamentoService);
    repository = module.get<Repository<gerenciamento_monitoramento>>(getRepositoryToken(gerenciamento_monitoramento));
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });

  describe('create', () => {
    it('should create a new record', async () => {
      const dto: CreateGerenciamentoDto = {
        status: 1,
        tipo: 'tipo',
        codigo_solicitacao: 'codigo',
        area: 100,
        modulo_fiscal: 50,
        progresso: 75,
        municipio: 'cidade',
        regional: 'região',
        anexo: 'anexo',
        criacao: new Date('2024-01-01')
      };

      const createdRecord = { ...dto, id: 1, criacao: new Date() };
      mockRepository.create.mockReturnValue(createdRecord);
      mockRepository.save.mockResolvedValue(createdRecord);

      const result = await service.create(dto);

      expect(result).toEqual(createdRecord);
      expect(mockRepository.create).toHaveBeenCalledWith({ ...dto, criacao: expect.any(Date) });
      expect(mockRepository.save).toHaveBeenCalledWith(createdRecord);
    });
  });

  describe('findAll', () => {
    it('should return paginated records', async () => {
      const records = [{ id: 1 }, { id: 2 }];
      mockRepository.findAndCount.mockResolvedValue([records, 2]);

      const result = await service.findAll();

      expect(result).toEqual({ data: records, total: 2 });
      expect(mockRepository.findAndCount).toHaveBeenCalledWith({
        skip: 0,
        take: 7,
      });
    });
  });

  describe('findOne', () => {
    it('should return a record if found', async () => {
      const record = { id: 1 };
      mockRepository.findOneBy.mockResolvedValue(record);

      const result = await service.findOne(1);

      expect(result).toEqual(record);
      expect(mockRepository.findOneBy).toHaveBeenCalledWith({ id: 1 });
    });

    it('should throw NotFoundException if no record is found', async () => {
      mockRepository.findOneBy.mockResolvedValue(null);

      await expect(service.findOne(1)).rejects.toThrow(NotFoundException);
    });
  });

  describe('update', () => {
    it('should update an existing record', async () => {
      const existingRecord = { id: 1, status: 1 };
      const updateDto: UpdateGerenciamentoDto = {
        status: 2,
        tipo: 'tipo',
        codigo_solicitacao: 'codigo',
        area: 100,
        modulo_fiscal: 50,
        progresso: 75,
        municipio: 'cidade',
        regional: 'região',
        anexo: 'anexo',
        atualizacao: new Date('2024-01-02'),

      };

      mockRepository.findOneBy.mockResolvedValue(existingRecord);
      mockRepository.save.mockResolvedValue({ ...existingRecord, ...updateDto });

      const result = await service.update(1, updateDto);

      expect(result).toEqual({ ...existingRecord, ...updateDto, atualizacao: expect.any(Date) });
      expect(mockRepository.save).toHaveBeenCalledWith({
        ...existingRecord,
        ...updateDto,
        atualizacao: expect.any(Date),
      });
    });

    it('should throw NotFoundException if no record is found', async () => {
      mockRepository.findOneBy.mockResolvedValue(null);

      await expect(service.update(1, { 
        status: 2,
        tipo: 'tipo',
        codigo_solicitacao: 'codigo',
        area: 100,
        modulo_fiscal: 50,
        progresso: 75,
        municipio: 'cidade',
        regional: 'região',
        anexo: 'anexo',
        atualizacao: new Date('2024-01-02'),
       })).rejects.toThrow(NotFoundException);
    });
  });

  describe('remove', () => {
    it('should remove a record if found', async () => {
      mockRepository.delete.mockResolvedValue({ affected: 1 });

      const result = await service.remove(1);

      expect(result).toBe('ID 1 excluído com sucesso');
      expect(mockRepository.delete).toHaveBeenCalledWith(1);
    });

    it('should throw NotFoundException if no record is found', async () => {
      mockRepository.delete.mockResolvedValue({ affected: 0 });

      await expect(service.remove(1)).rejects.toThrow(NotFoundException);
    });
  });
});