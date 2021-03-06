package com.xcv58.spec_board.android.services;

import android.app.IntentService;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;

import com.xcv58.spec_board.android.utils.Utils;

/**
 * An {@link IntentService} subclass for handling asynchronous task requests in
 * a service on a separate handler thread.
 * <p/>
 * TODO: Customize class - update intent actions, extra parameters and static
 * helper methods.
 */
public class SPECIntentService extends IntentService {
    public static final String STOP = "STOP";
    public static final String START = "START";

    public static boolean CONTINUE = false;
    public static String task;

    public SPECIntentService() {
        super("SPECIntentService");
    }

    @Override
    protected void onHandleIntent(Intent intent) {
        if (intent != null) {
            final String action = intent.getAction();
            Log.d(Utils.TAG, action);
            Utils.debug("receive " + action);
            Bundle bundle = intent.getExtras();
            if (bundle != null) {
                for (String key : bundle.keySet()) {
                    Utils.debug(key + ": " + bundle.getString(key));
                    if (START.equals(key)) {
                        Utils.debug(START);
                        if (CONTINUE) {
                            // TODO: already running, update task
                            this.updateTask();
                        } else {
                            // TODO: make something running
                            CONTINUE = true;
                            this.start();
                        }
                    } else if (STOP.equals(key)) {
                        Utils.debug(STOP);
                        CONTINUE = false;
                        this.stop();
                    }
                }
            }
        }
    }

    private void updateTask() {

    }

    private void start() {
        Utils.debug("start() start");
//        benchmarkTask.execute();
//        benchmarkTask.doInBackground(null);
        Utils.start();
        Utils.debug("start() end");
    }

    private void stop() {
        Utils.stop();
    }
}
