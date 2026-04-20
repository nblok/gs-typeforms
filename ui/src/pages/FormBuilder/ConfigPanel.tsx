import {
  Box,
  Button,
  Checkbox,
  Divider,
  FormControlLabel,
  IconButton,
  Stack,
  TextField,
  Typography,
} from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import AddIcon from '@mui/icons-material/Add';
import TouchAppIcon from '@mui/icons-material/TouchApp';
import type { FieldDefinition } from '../../types/fieldDefinition';
import type { FormField } from './formField';

interface Props {
  field: FormField | null;
  fieldDefinitions: FieldDefinition[];
  onChange: (field: FormField) => void;
}

export function ConfigPanel({ field, fieldDefinitions, onChange }: Props) {
  const title = field
    ? `Configure · ${fieldDefinitions.find((d) => d.type === field.type)?.label}`
    : 'Configuration';

  return (
    <Box
      sx={{
        width: 260,
        bgcolor: 'background.paper',
        borderLeft: 1,
        borderColor: 'divider',
        display: 'flex',
        flexDirection: 'column',
        flexShrink: 0,
        overflow: 'auto',
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
          borderBottom: 1,
          borderColor: 'divider',
        }}
      >
        {title}
      </Typography>

      {!field ? (
        <Box
          sx={{ textAlign: 'center', mt: 8, px: 2, color: 'text.secondary' }}
        >
          <TouchAppIcon sx={{ fontSize: 32, mb: 1 }} />
          <Typography variant="body2">Select a field to configure it</Typography>
        </Box>
      ) : (
        <ConfigFields field={field} onChange={onChange} />
      )}
    </Box>
  );
}

interface ConfigFieldsProps {
  field: FormField;
  onChange: (field: FormField) => void;
}

function ConfigFields({ field, onChange }: ConfigFieldsProps) {
  const updateLabel = (label: string) => onChange({ ...field, label });
  const updateRequired = (required: boolean) =>
    onChange({ ...field, required });

  return (
    <Stack spacing={2} sx={{ p: 1.75 }}>
      <TextField
        label="Question label"
        size="small"
        fullWidth
        value={field.label}
        onChange={(e) => updateLabel(e.target.value)}
      />

      <FormControlLabel
        control={
          <Checkbox
            size="small"
            checked={field.required}
            onChange={(e) => updateRequired(e.target.checked)}
          />
        }
        label={<Typography variant="body2">Required</Typography>}
      />

      <Divider />

      {(field.type === 'short_text' || field.type === 'long_text') && (
        <>
          <TextField
            label="Placeholder"
            size="small"
            fullWidth
            value={field.config.placeholder}
            onChange={(e) =>
              onChange({
                ...field,
                config: { ...field.config, placeholder: e.target.value },
              })
            }
          />
          <TextField
            label="Max length (optional)"
            size="small"
            fullWidth
            type="number"
            placeholder="No limit"
            value={field.config.maxLength ?? ''}
            onChange={(e) =>
              onChange({
                ...field,
                config: {
                  ...field.config,
                  maxLength: e.target.value ? Number(e.target.value) : null,
                },
              })
            }
          />
        </>
      )}

      {field.type === 'multiple_choice' && (
        <>
          <Box>
            <Typography
              variant="overline"
              color="text.secondary"
              sx={{ display: 'block', mb: 0.75 }}
            >
              Options
            </Typography>
            <Stack spacing={0.75}>
              {field.config.options.map((opt, i) => (
                <Stack
                  key={i}
                  direction="row"
                  spacing={0.5}
                  sx={{ alignItems: 'center' }}
                >
                  <TextField
                    size="small"
                    fullWidth
                    value={opt}
                    onChange={(e) => {
                      const options = [...field.config.options];
                      options[i] = e.target.value;
                      onChange({
                        ...field,
                        config: { ...field.config, options },
                      });
                    }}
                  />
                  <IconButton
                    size="small"
                    disabled={field.config.options.length <= 2}
                    onClick={() =>
                      onChange({
                        ...field,
                        config: {
                          ...field.config,
                          options: field.config.options.filter(
                            (_, j) => j !== i,
                          ),
                        },
                      })
                    }
                    aria-label="Remove option"
                  >
                    <CloseIcon fontSize="small" />
                  </IconButton>
                </Stack>
              ))}
            </Stack>
            <Button
              size="small"
              startIcon={<AddIcon />}
              sx={{ mt: 1, textTransform: 'none' }}
              onClick={() =>
                onChange({
                  ...field,
                  config: {
                    ...field.config,
                    options: [
                      ...field.config.options,
                      `Option ${field.config.options.length + 1}`,
                    ],
                  },
                })
              }
            >
              Add option
            </Button>
          </Box>
          <FormControlLabel
            control={
              <Checkbox
                size="small"
                checked={field.config.allowMultiple}
                onChange={(e) =>
                  onChange({
                    ...field,
                    config: {
                      ...field.config,
                      allowMultiple: e.target.checked,
                    },
                  })
                }
              />
            }
            label={
              <Typography variant="body2">Allow multiple selections</Typography>
            }
          />
        </>
      )}

      {field.type === 'yes_no' && (
        <Stack direction="row" spacing={1}>
          <TextField
            label="True label"
            size="small"
            fullWidth
            value={field.config.trueLabel}
            onChange={(e) =>
              onChange({
                ...field,
                config: { ...field.config, trueLabel: e.target.value },
              })
            }
          />
          <TextField
            label="False label"
            size="small"
            fullWidth
            value={field.config.falseLabel}
            onChange={(e) =>
              onChange({
                ...field,
                config: { ...field.config, falseLabel: e.target.value },
              })
            }
          />
        </Stack>
      )}

      {field.type === 'rating' && (
        <>
          <TextField
            label="Scale (max value)"
            size="small"
            fullWidth
            type="number"
            slotProps={{ htmlInput: { min: 3, max: 10 } }}
            value={field.config.maxValue}
            onChange={(e) =>
              onChange({
                ...field,
                config: { ...field.config, maxValue: Number(e.target.value) },
              })
            }
          />
          <TextField
            label="Label"
            size="small"
            fullWidth
            value={field.config.label}
            onChange={(e) =>
              onChange({
                ...field,
                config: { ...field.config, label: e.target.value },
              })
            }
          />
        </>
      )}
    </Stack>
  );
}
