import {
  Box,
  IconButton,
  Paper,
  Stack,
  Typography,
  alpha,
} from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import type { FieldDefinition } from '../../types/fieldDefinition';
import { FIELD_TYPE_META } from './fieldTypeMeta';
import { FieldPreview } from './FieldPreview';
import type { FormField } from './formField';

interface Props {
  field: FormField;
  order: number;
  selected: boolean;
  fieldDefinitions: FieldDefinition[];
  onClick: () => void;
  onDelete: () => void;
}

export function FieldCard({
  field,
  order,
  selected,
  fieldDefinitions,
  onClick,
  onDelete,
}: Props) {
  const { color, Icon } = FIELD_TYPE_META[field.type];
  const def = fieldDefinitions.find((d) => d.type === field.type);

  return (
    <Paper
      onClick={onClick}
      variant="outlined"
      sx={{
        p: 1.5,
        cursor: 'pointer',
        borderWidth: 2,
        borderColor: selected ? color : 'divider',
        boxShadow: selected ? `0 0 0 3px ${alpha(color, 0.2)}` : undefined,
        transition: 'border-color 0.15s, box-shadow 0.15s',
      }}
    >
      <Stack direction="row" spacing={1.25} sx={{ alignItems: 'center' }}>
        <Typography
          variant="caption"
          color="text.secondary"
          sx={{ minWidth: 18 }}
        >
          {order}
        </Typography>
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
        <Box sx={{ flex: 1, minWidth: 0 }}>
          <Typography
            variant="body2"
            sx={{
              fontWeight: 600,
              whiteSpace: 'nowrap',
              overflow: 'hidden',
              textOverflow: 'ellipsis',
            }}
          >
            {field.label || (
              <Box component="span" sx={{ color: 'text.secondary' }}>
                Untitled question
              </Box>
            )}
            {field.required && (
              <Box component="span" sx={{ color: 'error.main', ml: 0.5 }}>
                *
              </Box>
            )}
          </Typography>
          <Typography variant="caption" color="text.secondary">
            {def?.label}
          </Typography>
        </Box>
        <IconButton
          size="small"
          onClick={(e) => {
            e.stopPropagation();
            onDelete();
          }}
          aria-label="Delete field"
        >
          <CloseIcon fontSize="small" />
        </IconButton>
      </Stack>

      {selected && (
        <Box
          sx={{
            mt: 1.5,
            pt: 1.5,
            borderTop: 1,
            borderColor: alpha(color, 0.25),
          }}
        >
          <FieldPreview field={field} />
        </Box>
      )}
    </Paper>
  );
}
