import {
  Checkbox,
  FormControl,
  FormControlLabel,
  FormLabel,
  Radio,
  RadioGroup,
  Rating,
  Stack,
  TextField,
  ToggleButton,
  ToggleButtonGroup,
} from '@mui/material';
import type { ParticipateFormField, AnswerValue } from '../../types/response';

interface Props {
  field: ParticipateFormField;
  value: AnswerValue | undefined;
  onChange: (value: AnswerValue) => void;
}

export function FieldInput({ field, value, onChange }: Props) {
  switch (field.type) {
    case 'short_text':
      return (
        <TextField
          fullWidth
          required={field.required}
          placeholder={field.config.placeholder}
          value={typeof value === 'string' ? value : ''}
          onChange={(e) => onChange(e.target.value)}
          slotProps={{
            htmlInput: { maxLength: field.config.maxLength ?? undefined },
          }}
        />
      );
    case 'long_text':
      return (
        <TextField
          fullWidth
          multiline
          minRows={4}
          required={field.required}
          placeholder={field.config.placeholder}
          value={typeof value === 'string' ? value : ''}
          onChange={(e) => onChange(e.target.value)}
          slotProps={{
            htmlInput: { maxLength: field.config.maxLength ?? undefined },
          }}
        />
      );
    case 'multiple_choice':
      if (field.config.allowMultiple) {
        const selected = Array.isArray(value) ? value : [];
        const toggle = (opt: string) => {
          const next = selected.includes(opt)
            ? selected.filter((o) => o !== opt)
            : [...selected, opt];
          onChange(next);
        };
        return (
          <FormControl component="fieldset">
            <Stack>
              {field.config.options.map((opt) => (
                <FormControlLabel
                  key={opt}
                  control={
                    <Checkbox
                      checked={selected.includes(opt)}
                      onChange={() => toggle(opt)}
                    />
                  }
                  label={opt}
                />
              ))}
            </Stack>
          </FormControl>
        );
      }
      return (
        <RadioGroup
          value={typeof value === 'string' ? value : ''}
          onChange={(e) => onChange(e.target.value)}
        >
          {field.config.options.map((opt) => (
            <FormControlLabel
              key={opt}
              value={opt}
              control={<Radio />}
              label={opt}
            />
          ))}
        </RadioGroup>
      );
    case 'yes_no':
      return (
        <ToggleButtonGroup
          exclusive
          value={typeof value === 'boolean' ? value : null}
          onChange={(_, v: boolean | null) => {
            if (v !== null) onChange(v);
          }}
        >
          <ToggleButton value={true}>{field.config.trueLabel}</ToggleButton>
          <ToggleButton value={false}>{field.config.falseLabel}</ToggleButton>
        </ToggleButtonGroup>
      );
    case 'rating':
      return (
        <FormControl>
          <FormLabel sx={{ mb: 1 }}>{field.config.label}</FormLabel>
          <Rating
            max={field.config.maxValue}
            value={typeof value === 'number' ? value : null}
            onChange={(_, v) => {
              if (v !== null) onChange(v);
            }}
          />
        </FormControl>
      );
  }
}
