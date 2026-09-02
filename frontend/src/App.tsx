import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { MapPage } from './pages/MapPage';
import { FortDetailsPage } from './pages/FortDetailsPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<MapPage />} />
        <Route path="/fort/:id" element={<FortDetailsPage />} />
      </Routes>
    </Router>
  );
}

export default App;
