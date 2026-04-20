import {
  Box,
  Checkbox,
  FormControlLabel,
  Radio,
  Stack,
  TextField,
  Typography,
} from '@mui/material';
import type { FormField } from './formField';

interface Props {
  field: FormField;
}

export function FieldPreview({ field }: Props) {
  switch (field.type) {
    case 'short_text':
      return (
        <TextField
          size="small"
          fullWidth
          disabled
          placeholder={field.config.placeholder}
        />
      );
    case 'long_text':
      return (
        <TextField
          size="small"
          fullWidth
          disabled
          multiline
          minRows={3}
          placeholder={field.config.placeholder}
        />
      );
    case 'multiple_choice':
      return (
        <Stack spacing={0.5}>
          {field.config.options.map((opt, i) => (
            <FormControlLabel
              key={i}
              disabled
              control={
                field.config.allowMultiple ? (
                  <Checkbox size="small" />
                ) : (
                  <Radio size="small" />
                )
              }
              label={<Typography variant="body2">{opt}</Typography>}
            />
          ))}
        </Stack>
      );
    case 'yes_no':
      return (
        <Stack direction="row" spacing={1}>
          {[field.config.trueLabel, field.config.falseLabel].map((lbl) => (
            <Box
              key={lbl}
              sx={{
                border: 1,
                borderColor: 'divider',
                borderRadius: 1,
                px: 2,
                py: 0.75,
                bgcolor: 'grey.50',
              }}
            >
              <Typography variant="body2" color="text.secondary">
                {lbl}
              </Typography>
            </Box>
          ))}
        </Stack>
      );
    case 'rating':
      return (
        <Stack direction="row" spacing={0.75}>
          {Array.from({ length: field.config.maxValue }, (_, i) => (
            <Box
              key={i}
              sx={{
                width: 28,
                height: 28,
                borderRadius: 1,
                border: 1,
                borderColor: 'divider',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                bgcolor: 'grey.50',
                color: 'text.secondary',
                fontSize: 12,
              }}
            >
              {i + 1}
            </Box>
          ))}
        </Stack>
      );
  }
}
