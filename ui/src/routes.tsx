import { createBrowserRouter } from 'react-router-dom';
import { Typography } from '@mui/material';
import LayoutPage from './pages/Layout/LayoutPage';
import FormsListPage from './pages/FormsList/FormsListPage';
import FormBuilderPage from './pages/FormBuilder/FormBuilderPage';
import ParticipatePage from './pages/Participate/ParticipatePage';
import FormResultsPage from './pages/FormResults/FormResultsPage';

export const router = createBrowserRouter([
  {
    element: <LayoutPage />,
    children: [
      { index: true, element: <FormsListPage /> },
      { path: 'builder', element: <FormBuilderPage /> },
      { path: 'forms/:formId/participate', element: <ParticipatePage /> },
      { path: 'forms/:formId/results', element: <FormResultsPage /> },
      { path: '*', element: <Typography>Page Not Found</Typography> },
    ],
  },
]);
