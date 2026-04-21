import {
  Alert,
  Box,
  CircularProgress,
  Container,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Typography,
} from '@mui/material';
import { useParams } from 'react-router-dom';
import { useParticipateForm } from '../../api/useParticipateForm';
import { useResponsesForForm } from '../../api/useResponse';
import type { AnswerValue, ParticipateFormField } from '../../types/response';

function renderAnswer(value: AnswerValue | undefined): string {
  if (value === undefined || value === null) return '';
  if (Array.isArray(value)) return value.join(', ');
  return String(value);
}

export default function FormResultsPage() {
  const { formId } = useParams<{ formId: string }>();
  const {
    data: form,
    isPending: formPending,
    isError: formError,
  } = useParticipateForm(formId);
  const {
    data: responses,
    isPending: responsesPending,
    isError: responsesError,
  } = useResponsesForForm(formId);

  if (formPending || responsesPending)
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Box>
    );
  if (formError || !form)
    return <Alert severity="error">Failed to load form.</Alert>;
  if (responsesError || !responses)
    return <Alert severity="error">Failed to load responses.</Alert>;

  const orderedFields: ParticipateFormField[] = [...form.fields].sort(
    (a, b) => a.order - b.order,
  );

  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 2 }}>
        <Typography variant="h4">Results: {form.title}</Typography>
      </Box>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>User ID</TableCell>
            {orderedFields.map((field) => (
              <TableCell key={field.id}>{field.label}</TableCell>
            ))}
          </TableRow>
        </TableHead>
        <TableBody>
          {responses.map((response) => (
            <TableRow key={response.id}>
              <TableCell>{response.respondentId}</TableCell>
              {orderedFields.map((field) => (
                <TableCell key={field.id}>
                  {renderAnswer(response.answers[field.id])}
                </TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>
      {responses.length === 0 && (
        <Box sx={{ mt: 2 }}>
          <Typography variant="body2" color="text.secondary">
            No responses yet.
          </Typography>
        </Box>
      )}
    </Container>
  );
}