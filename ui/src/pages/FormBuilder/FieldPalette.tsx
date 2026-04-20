import { Box, ButtonBase, Stack, Typography, alpha } from '@mui/material';
import type { FieldDefinition, FieldType } from '../../types/fieldDefinition';
import { FIELD_TYPE_META } from './fieldTypeMeta';

interface Props {
  fieldDefinitions: FieldDefinition[];
  onAddField: (type: FieldType) => void;
}

export function FieldPalette({ fieldDefinitions, onAddField }: Props) {
  return (
    <Box
      sx={{
        width: 220,
        bgcolor: 'background.paper',
        borderRight: 1,
        borderColor: 'divider',
        display: 'flex',
        flexDirection: 'column',
        flexShrink: 0,
      }}
    >
      <Typography
        variant="overline"
        sx={{
          px: 1.75,
          pt: 1.75,
          pb: 1,
          color: 'text.secondary',
          fontWeight: 600,
          letterSpacing: '0.08em',
        }}
      >
        Field types
      </Typography>
      <Stack spacing={0.25} sx={{ px: 1, pb: 1 }}>
        {fieldDefinitions.map((def) => {
          const { color, Icon } = FIELD_TYPE_META[def.type];
          return (
            <ButtonBase
              key={def.type}
              onClick={() => onAddField(def.type)}
              sx={{
                display: 'flex',
                alignItems: 'center',
                gap: 1.25,
                p: 1,
                borderRadius: 1,
                justifyContent: 'flex-start',
                textAlign: 'left',
                transition: 'background 0.12s',
                '&:hover': { bgcolor: 'action.hover' },
              }}
            >
              <Box
                sx={{
                  width: 28,
                  height: 28,
                  borderRadius: 1,
                  bgcolor: alpha(color, 0.12),
                  color,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  flexShrink: 0,
                }}
              >
                <Icon sx={{ fontSize: 18 }} />
              </Box>
              <Box sx={{ minWidth: 0 }}>
                <Typography
                  variant="body2"
                  sx={{ fontWeight: 600, lineHeight: 1.2 }}
                >
                  {def.label}
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  {def.description}
                </Typography>
              </Box>
            </ButtonBase>
          );
        })}
      </Stack>
    </Box>
  );
}
