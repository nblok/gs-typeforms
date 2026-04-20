import { Alert, AlertTitle, Typography } from '@mui/material';

interface Props {
  error: Error;
}

export function ErrorAlert({ error }: Props) {
  return (
    <Alert severity="error">
      <AlertTitle>Something went wrong</AlertTitle>
      <Typography component="p">{error.message}</Typography>
    </Alert>
  );
}
