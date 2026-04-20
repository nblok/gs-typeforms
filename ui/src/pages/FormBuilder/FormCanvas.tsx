import { Box, Button, Paper, Stack, Typography } from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import type { FieldDefinition, FieldType } from '../../types/fieldDefinition';
import { FIELD_TYPE_META } from './fieldTypeMeta';
import { FieldCard } from './FieldCard';
import type { FormField } from './formField';

interface Props {
  formTitle: string;
  fields: FormField[];
  selectedId: number | null;
  fieldDefinitions: FieldDefinition[];
  onSelectField: (id: number | null) => void;
  onDeleteField: (id: number) => void;
  onAddField: (type: FieldType) => void;
}

export function FormCanvas({
  formTitle,
  fields,
  selectedId,
  fieldDefinitions,
  onSelectField,
  onDeleteField,
  onAddField,
}: Props) {
  return (
    <Box
      sx={{
        flex: 1,
        overflow: 'auto',
        p: 3,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
      }}
    >
      <Box sx={{ width: '100%', maxWidth: 560 }}>
        <Paper variant="outlined" sx={{ p: 2.5, mb: 2, borderRadius: 2 }}>
          <Typography variant="h6" sx={{ fontWeight: 700 }}>
            {formTitle || 'Untitled form'}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {fields.length} question{fields.length !== 1 ? 's' : ''}
          </Typography>
        </Paper>

        {fields.length === 0 ? (
          <Box sx={{ textAlign: 'center', py: 8, color: 'text.secondary' }}>
            <AddIcon sx={{ fontSize: 40, mb: 1.5 }} />
            <Typography variant="body1" sx={{ fontWeight: 500 }}>
              Add your first field
            </Typography>
            <Typography variant="body2" sx={{ mt: 0.5 }}>
              Click a field type on the left to get started
            </Typography>
          </Box>
        ) : (
          <Stack spacing={1.25}>
            {fields.map((f, i) => (
              <FieldCard
                key={f.id}
                field={f}
                order={i + 1}
                selected={f.id === selectedId}
                fieldDefinitions={fieldDefinitions}
                onClick={() => onSelectField(f.id === selectedId ? null : f.id)}
                onDelete={() => onDeleteField(f.id)}
              />
            ))}
            <Stack
              direction="row"
              spacing={1}
              sx={{ flexWrap: 'wrap', mt: 0.5, gap: 1 }}
            >
              {fieldDefinitions.map((def) => {
                const { color, Icon } = FIELD_TYPE_META[def.type];
                return (
                  <Button
                    key={def.type}
                    size="small"
                    variant="outlined"
                    onClick={() => onAddField(def.type)}
                    startIcon={<Icon sx={{ color, fontSize: 16 }} />}
                    sx={{
                      borderStyle: 'dashed',
                      color: 'text.secondary',
                      textTransform: 'none',
                    }}
                  >
                    {def.label}
                  </Button>
                );
              })}
            </Stack>
          </Stack>
        )}
      </Box>
    </Box>
  );
}
