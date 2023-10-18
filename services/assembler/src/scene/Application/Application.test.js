import Application from './App';
import React from 'react';
import ReactDOM from 'react-dom';
import MemoryRouter from 'react-router-dom/MemoryRouter';

describe('<App />', () => {
  test('renders without exploding', () => {
    const div = document.createElement('div');
    ReactDOM.render(
      <MemoryRouter>
        <Application />
      </MemoryRouter>,
      div
    );
  });
});
