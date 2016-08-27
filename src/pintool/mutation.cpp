VOID randomMutation()
{
    sleep(1);
    srand(time(NULL));
    fuzzValue = (rand() % (0xffffffff - KnobStartValue.Value())) + KnobStartValue.Value();
}


VOID stepMutation()
{
    cout << "fuzzing value " << fuzzValue << endl;
    fuzzValue += 0x10;
    cout << "fuzzing value " << fuzzValue << endl;
}


VOID mutateREG(CONTEXT *ctx, ADDRINT nextInsAddr, ADDRINT callAddr)
{
  if (KnobFuzzType.Value() == "random")
      randomMutation();
  else if (KnobFuzzType.Value() == "inc")
      fuzzValue++;
  else
      fuzzValue = fuzzValue;

  PIN_SetContextReg(ctx, LEVEL_BASE::REG_RIP, KnobStart.Value());
}


void update_context(CONTEXT *ctx, int parindex, int fuzzcount)
{
  int index = parindex*6 + fuzzcount;
  cout << "i am " << index << endl;
  
  UINT64 *arr = fuzzing_context[index];

  cout << "i am " << arr << endl;
  int i = 0;
  int l = sizeof(parList)/sizeof(UINT32);

  for (i = 0; i< l; i++)
    {
      REG r = intputRegsRef[i];
      UINT64 fv = arr[i];

      PIN_SetContextReg(ctx, r, fv);
    }

  displayCurrentContext(ctx, CONTEXT_FLG);
  return;
}


void mutate_ctx(CONTEXT *ctx)
{
  cout << "FUZZCOUNT " << fuzzCount << " PARINDEX " << parIndex << endl;
  if (fuzzCount == 0)
    {
      if (parIndex >= sizeof(parList)/sizeof(UINT32))
        {
          PIN_SetContextReg(ctx, LEVEL_BASE::REG_RIP, KnobStart.Value());
          return;
        }
    }

  update_context(ctx, parIndex, fuzzCount);

  fuzzCount++;
  if (fuzzCount == KnobFuzzCount.Value())
    {
      parIndex++;
      fuzzCount = 0;
    }
}

VOID mutate(CONTEXT *ctx)
{
    cout << "FUZZCOUNT " << fuzzCount << " PARINDEX " << parIndex << endl;
    if (fuzzCount == 0)
    {
        if (parIndex >= sizeof(parList)/sizeof(UINT32))
        {
            PIN_SetContextReg(ctx, LEVEL_BASE::REG_RIP, KnobStart.Value());
            return;
        }

        REG r = regsRef[parList[parIndex]].ref;
        fuzzValue = PIN_GetContextReg(ctx, r);
    }

    if (KnobFuzzType.Value() == "random")
        randomMutation();
    else if (KnobFuzzType.Value() == "inc")
        fuzzValue++;
    else if (KnobFuzzType.Value() == "step")
        stepMutation();
    else
        fuzzValue = fuzzValue;

    REG r = regsRef[parList[parIndex]].ref;
    PIN_SetContextReg(ctx, r, fuzzValue);
    fuzzCount++;
    if (fuzzCount == KnobFuzzCount.Value())
    {
        parIndex++;
        fuzzCount = 0;
    }
}
