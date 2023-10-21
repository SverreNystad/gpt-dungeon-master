import React from 'react';

const Quit = () => {
  return (
    <>
        <p>You have exited</p>
        {window.close()}
    </>
  );
}

export default Quit;
