import { createBrowserRouter } from 'react-router-dom';
import { Typography } from '@mui/material';
import LayoutPage from './pages/Layout/LayoutPage';
import FormsListPage from './pages/FormsList/FormsListPage';
import FormBuilderPage from './pages/FormBuilder/FormBuilderPage';

export const router = createBrowserRouter([
  {
    element: <LayoutPage />,
    children: [
      { index: true, element: <FormsListPage /> },
      { path: 'builder', element: <FormBuilderPage /> },
      { path: '*', element: <Typography>Page Not Found</Typography> },
    ],
  },
]);
