void finishFuzzing(CONTEXT *ctx);

void startFuzzing(CONTEXT *ctx, ADDRINT nextInsAddr, ADDRINT callNext);

void stopFuzzing(CONTEXT *ctx);

void resumeFromStart(CONTEXT *ctx);
