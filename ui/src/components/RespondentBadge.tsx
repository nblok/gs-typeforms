import { Box, Button, Typography } from '@mui/material';
import { useRespondentId } from '../utils/useRespondentId';

export function RespondentBadge() {
  const [respondentId, regenerate] = useRespondentId();

  return (
    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5 }}>
      <Typography variant="body2" sx={{ fontFamily: 'monospace' }}>
        {respondentId ? `User: ${respondentId.slice(0, 8)}` : 'User: —'}
      </Typography>
      <Button
        onClick={regenerate}
        size="small"
        variant="outlined"
        color="inherit"
      >
        New user
      </Button>
    </Box>
  );
}
