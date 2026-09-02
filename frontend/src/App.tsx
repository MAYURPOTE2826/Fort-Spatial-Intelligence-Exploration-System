import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { MapPage } from './pages/MapPage';
import { FortDetailsPage } from './pages/FortDetailsPage';
import { NetworkPage } from './pages/NetworkPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<MapPage />} />
        <Route path="/fort/:id" element={<FortDetailsPage />} />
        <Route path="/network" element={<NetworkPage />} />
      </Routes>
    </Router>
  );
}

export default App;
