import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Box, CircularProgress } from '@mui/material';
import type { FieldDefinition, FieldType } from '../../types/fieldDefinition';
import { useFieldDefinitions } from '../../api/useFieldDefinitions';
import { ErrorAlert } from '../../components/ErrorAlert';
import { BuilderTopBar } from './BuilderTopBar';
import { FieldPalette } from './FieldPalette';
import { FormCanvas } from './FormCanvas';
import { ConfigPanel } from './ConfigPanel';
import type { FormField } from './formField';

let nextId = 1;

function buildField(
  type: FieldType,
  fieldDefinitions: FieldDefinition[],
): FormField | null {
  const def = fieldDefinitions.find((d) => d.type === type);
  if (!def) return null;
  const base = {
    id: nextId++,
    label: `${def.label} question`,
    required: false,
  };
  switch (def.type) {
    case 'short_text':
      return { ...base, type: 'short_text', config: { ...def.defaultConfig } };
    case 'long_text':
      return { ...base, type: 'long_text', config: { ...def.defaultConfig } };
    case 'multiple_choice':
      return {
        ...base,
        type: 'multiple_choice',
        config: {
          ...def.defaultConfig,
          options: [...def.defaultConfig.options],
        },
      };
    case 'yes_no':
      return { ...base, type: 'yes_no', config: { ...def.defaultConfig } };
    case 'rating':
      return { ...base, type: 'rating', config: { ...def.defaultConfig } };
  }
}

export default function FormBuilderPage() {
  const navigate = useNavigate();
  const { data: fieldDefinitions, isPending, error } = useFieldDefinitions();
  const [formTitle, setFormTitle] = useState('Untitled form');
  const [fields, setFields] = useState<FormField[]>([]);
  const [selectedId, setSelectedId] = useState<number | null>(null);

  const handleCancel = () => navigate('/');
  const handlePublish = () => navigate('/');

  if (isPending) {
    return (
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          height: '100%',
        }}
      >
        <CircularProgress />
      </Box>
    );
  }
  if (error) return <ErrorAlert error={error} />;
  if (!fieldDefinitions) return null;

  const selected = fields.find((f) => f.id === selectedId) ?? null;

  const addField = (type: FieldType) => {
    const newField = buildField(type, fieldDefinitions);
    if (!newField) return;
    setFields((prev) => [...prev, newField]);
    setSelectedId(newField.id);
  };

  const updateField = (updated: FormField) =>
    setFields((prev) => prev.map((f) => (f.id === updated.id ? updated : f)));

  const deleteField = (id: number) => {
    setFields((prev) => prev.filter((f) => f.id !== id));
    if (selectedId === id) setSelectedId(null);
  };

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        height: '100%',
        bgcolor: 'grey.100',
      }}
    >
      <BuilderTopBar
        formTitle={formTitle}
        onFormTitleChange={setFormTitle}
        onCancel={handleCancel}
        onPublish={handlePublish}
      />
      <Box sx={{ display: 'flex', flex: 1, overflow: 'hidden' }}>
        <FieldPalette
          fieldDefinitions={fieldDefinitions}
          onAddField={addField}
        />
        <FormCanvas
          formTitle={formTitle}
          fields={fields}
          selectedId={selectedId}
          fieldDefinitions={fieldDefinitions}
          onSelectField={setSelectedId}
          onDeleteField={deleteField}
          onAddField={addField}
        />
        <ConfigPanel
          field={selected}
          fieldDefinitions={fieldDefinitions}
          onChange={updateField}
        />
      </Box>
    </Box>
  );
}
