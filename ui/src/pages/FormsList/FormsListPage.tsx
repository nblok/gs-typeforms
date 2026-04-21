import {
  Alert,
  Box,
  Button,
  CircularProgress,
  Container,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Typography,
  useTheme,
} from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import { useForms } from '../../api/useForms';
import { formatDate } from '../../utils/formatDate';

export default function FormsListPage() {
  const { data: forms, isPending, isError } = useForms();
  const theme = useTheme();

  return (
    <Container maxWidth="lg">
      <Box className="form-list-header">
        <Box
          sx={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            my: 2,
          }}
        >
          <Typography variant="h4">My Forms</Typography>
          <Box>
            <Button component={RouterLink} variant="contained" to="/builder">
              Create Form
            </Button>
          </Box>
        </Box>
      </Box>
      <Box className="form-list-forms">
        {isPending && <CircularProgress />}
        {isError && <Alert severity="error">Failed to load forms.</Alert>}
        {forms && (
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Title</TableCell>
                <TableCell>Created</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {forms.map((form) => (
                <TableRow key={form.id}>
                  <TableCell>{form.title}</TableCell>
                  <TableCell>
                    {form.createdAt ? formatDate(form.createdAt) : '—'}
                  </TableCell>
                  <TableCell>
                      <Box
                          sx={{
                            'display': 'flex',
                            'column-gap': theme.spacing(1),
                          }}
                      >
                        <Button
                          component={RouterLink}
                          to={`/forms/${form.id}/participate`}
                          variant="outlined"
                          size="small"
                        >
                          Participate
                        </Button>
                        <Button variant="outlined" size="small">
                          View Results
                        </Button>
                      </Box>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}
      </Box>
    </Container>
  );
}
