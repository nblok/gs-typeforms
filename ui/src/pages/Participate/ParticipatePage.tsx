import { useCallback, useEffect, useRef, useState } from 'react';
import { useParams } from 'react-router-dom';
import {
  Alert,
  Box,
  CircularProgress,
  Container,
  Stack,
  Typography,
} from '@mui/material';
import { useParticipateForm } from '../../api/useParticipateForm';
import { useResponse, useSubmitResponse } from '../../api/useResponse';
import { useRespondentId } from '../../utils/useRespondentId';
import { FieldInput } from './FieldInput';
import type { AnswerValue } from '../../types/response';

export default function ParticipatePage() {
  const { formId } = useParams<{ formId: string }>();
  const [respondentId] = useRespondentId();

  return (
    <Container maxWidth="md" sx={{ py: 3 }}>
      {respondentId && formId ? (
        <ParticipateContent
          key={respondentId}
          formId={formId}
          respondentId={respondentId}
        />
      ) : (
        <CircularProgress />
      )}
    </Container>
  );
}

interface ContentProps {
  formId: string;
  respondentId: string;
}

function ParticipateContent({ formId, respondentId }: ContentProps) {
  const {
    data: form,
    isPending: formPending,
    isError: formError,
  } = useParticipateForm(formId);
  const {
    data: existing,
    isPending: responsePending,
    isFetched: responseFetched,
  } = useResponse(formId, respondentId);
  const submit = useSubmitResponse(formId);

  const [answers, setAnswers] = useState<Record<string, AnswerValue>>({});
  const hydrated = useRef(false);

  useEffect(() => {
    if (responseFetched && !hydrated.current) {
      setAnswers(existing?.answers ?? {});
      hydrated.current = true;
    }
  }, [responseFetched, existing]);

  const submitMutate = submit.mutate;
  const timerRef = useRef<ReturnType<typeof setTimeout> | undefined>(undefined);
  useEffect(
    () => () => {
      if (timerRef.current) clearTimeout(timerRef.current);
    },
    [],
  );
  const debouncedSubmit = useCallback(
    (next: Record<string, AnswerValue>) => {
      if (timerRef.current) clearTimeout(timerRef.current);
      timerRef.current = setTimeout(() => {
        submitMutate({ respondentId, answers: next });
      }, 500);
    },
    [respondentId, submitMutate],
  );

  const handleChange = (fieldId: string, value: AnswerValue) => {
    const next = { ...answers, [fieldId]: value };
    setAnswers(next);
    debouncedSubmit(next);
  };

  if (formPending || responsePending) return <CircularProgress />;
  if (formError || !form)
    return <Alert severity="error">Failed to load form.</Alert>;

  return (
    <Box>
      <Typography variant="h4" sx={{ mb: 1 }}>
        {form.title}
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Your answers are saved automatically.
      </Typography>
      <Stack spacing={3}>
        {form.fields.map((field) => (
          <Box key={field.id}>
            <Typography variant="subtitle1" sx={{ mb: 1 }}>
              {field.label}
              {field.required && (
                <Typography
                  component="span"
                  color="error"
                  sx={{ ml: 0.5 }}
                >
                  *
                </Typography>
              )}
            </Typography>
            <FieldInput
              field={field}
              value={answers[field.id]}
              onChange={(v) => handleChange(field.id, v)}
            />
          </Box>
        ))}
      </Stack>
      {submit.isError && (
        <Alert severity="error" sx={{ mt: 2 }}>
          Failed to save answers.
        </Alert>
      )}
    </Box>
  );
}
